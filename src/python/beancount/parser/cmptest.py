"""Support utillities for testing scripts.
"""
import unittest
import io
import textwrap

from beancount.parser import parser
from beancount.parser import printer
from beancount.core import compare


class TestCase(unittest.TestCase):

    def assertEqualEntries(self, expected_entries, actual_entries):
        """Compare two lists of entries exactly and print missing entries verbosely if
        they occur.

        Args:
          expected_entries: Either a list of directives or a string, in which case the
            string is run through beancount.parser.parse_string() and the resulting
            list is used.
          actual_entries: Same treatment as expected_entries, the other list of
            directives to compare to.
        Raises:
          AssertionError: If the exception fails.
        """
        if isinstance(expected_entries, str):
            expected_entries, _, __ = parser.parse_string(textwrap.dedent(expected_entries))
        if isinstance(actual_entries, str):
            actual_entries, _, __ = parser.parse_string(textwrap.dedent(actual_entries))
        same, expected_missing, actual_missing = compare.compare_entries(expected_entries,
                                                                         actual_entries)
        if not same:
            assert expected_missing or actual_missing
            oss = io.StringIO()
            if expected_missing:
                oss.write("Missing from from first/expected set:\n\n")
                for entry in expected_missing:
                    oss.write(printer.format_entry(entry))
                    oss.write('\n')
            if actual_missing:
                oss.write("Missing from from actual:\n\n")
                for entry in actual_missing:
                    oss.write(printer.format_entry(entry))
                    oss.write('\n')
            self.fail(oss.getvalue())

    def assertIncludesEntries(self, subset_entries, entries):
        """Check that subset_entries is included in entries and print missing entries.

        Args:
          subset_entries: Either a list of directives or a string, in which case the
            string is run through beancount.parser.parse_string() and the resulting
            list is used.
          entries: Same treatment as subset_entries, the other list of
            directives to compare to.
        Raises:
          AssertionError: If the exception fails.
        """
        if isinstance(subset_entries, str):
            subset_entries, _, __ = parser.parse_string(textwrap.dedent(subset_entries))
        if isinstance(entries, str):
            entries, _, __ = parser.parse_string(textwrap.dedent(entries))
        includes, missing = compare.includes_entries(subset_entries, entries)
        if not includes:
            assert missing
            oss = io.StringIO()
            if missing:
                oss.write("Missing from from first/expected set:\n\n")
                for entry in missing:
                    oss.write(printer.format_entry(entry))
                    oss.write('\n')
            self.fail(oss.getvalue())

    def assertExcludesEntries(self, subset_entries, entries):
        """Check that subset_entries is not included in entries and print extra entries.

        Args:
          subset_entries: Either a list of directives or a string, in which case the
            string is run through beancount.parser.parse_string() and the resulting
            list is used.
          entries: Same treatment as subset_entries, the other list of
            directives to compare to.
        Raises:
          AssertionError: If the exception fails.
        """
        if isinstance(subset_entries, str):
            subset_entries, _, __ = parser.parse_string(textwrap.dedent(subset_entries))
        if isinstance(entries, str):
            entries, _, __ = parser.parse_string(textwrap.dedent(entries))
        excludes, extra = compare.excludes_entries(subset_entries, entries)
        if not excludes:
            assert extra
            oss = io.StringIO()
            if extra:
                oss.write("Extra from from first/excluded set:\n\n")
                for entry in extra:
                    oss.write(printer.format_entry(entry))
                    oss.write('\n')
            self.fail(oss.getvalue())
