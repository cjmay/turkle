import os
import sys


from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from hits.models import HitTemplate
from unicodecsv import DictWriter


def get_fieldnames(hit):
    return tuple(sorted(
        [u'Input.' + k for k in hit.input_csv_fields.keys()]
        + [u'Answer.' + k for k in hit.answers.keys()]
    ))


def results_data_groups(completed_hits):
    hit_fieldname_tuples = map(get_fieldnames, completed_hits)
    fieldname_tuple_id_map = dict(
        (t, i)
        for (i, t)
        in enumerate(sorted(set(hit_fieldname_tuples)))
    )

    hit_groups = [[] for t in fieldname_tuple_id_map] 
    for (hit, fieldnames) in zip(completed_hits, hit_fieldname_tuples):
        i = fieldname_tuple_id_map[fieldnames]
        hit_groups[i].append(hit)

    return map(results_data, hit_groups)


def results_data(completed_hits):
    """
    All completed HITs must come from the same template so that they have the
    same field names.
    """
    fieldnames = get_fieldnames(completed_hits[0])

    rows = []
    for hit in completed_hits:
        row = {}
        row.update({u'Input.' + k: v for k, v in hit.input_csv_fields.items()})
        row.update({u'Answer.' + k: v for k, v in hit.answers.items()})
        rows.append(row)

    return fieldnames, rows


class Command(BaseCommand):

    args = '<template_file_path> <results_csv_file_path>'
    help = (
        'Dumps results of the completed HITs for the template'
        ' <template_file_path> to a file at <results_csv_file_path>. '
		' If <template_file_path> is * then results will be written to'
		' a separate file for each template and unique set of'
		' fieldnames (<results_csv_file_path> will be interpreted as a'
		' prefix for the individual results files).'
    )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError(
                'usage: python manage.py dump_results '
                '<template_file_path> '
                '<results_csv_file_path>'
            )

        (template_file_path, results_csv_file_path) = args

        if template_file_path == '*':
            results_idx = 0
            for template in HitTemplate.objects.all():
                completed_hits = template.hit_set.filter(completed=True)

                if completed_hits.exists():
                    groups = results_data_groups(completed_hits)
                    for (fieldnames, rows) in groups:
                        real_results_path = (
                            '%s.%d.csv' % (results_csv_file_path, results_idx)
                        )
                        with open(real_results_path, 'wb') as fh:
                            writer = DictWriter(fh, fieldnames)
                            writer.writeheader()
                            for row in rows:
                                writer.writerow(row)

                        results_idx += 1

        else:
            template_file_path = os.path.abspath(template_file_path)
            results_csv_file_path = os.path.abspath(results_csv_file_path)

            try:
                template = HitTemplate.objects.get(name=template_file_path)
            except ObjectDoesNotExist:
                sys.exit('There is no matching <template_file_path>.')

            completed_hits = template.hit_set.filter(completed=True)
            if not completed_hits.exists():
                sys.exit('There are no completed HITs.')

            (fieldnames, rows) = results_data(completed_hits)
            with open(results_csv_file_path, 'wb') as fh:
                writer = DictWriter(fh, fieldnames)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
