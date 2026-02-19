import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class TableStitcher:
    """Fixes tables split across multiple pages (LOAN-BUG-001)."""

    def __init__(self):
        self.merge_count = 0

    def columns_match(self, table1, table2):
        """Check if two tables have the same column headers."""
        if not table1 or not table2:
            return False
        headers1 = table1[0].keys()
        headers2 = table2[0].keys()
        return set(headers1) == set(headers2)

    def stitch_tables(self, tables_by_page):
        """Merge tables that span across pages."""
        if not tables_by_page:
            return []
        
        merged_tables = []
        current_table = None

        for page_num, tables in tables_by_page.items():
            for table in tables:
                if current_table is None:
                    current_table = table
                elif self.columns_match(current_table, table):
                    current_table = current_table + table
                    self.merge_count += 1
                    logger.info(f"Merged table from page {page_num}")
                else:
                    merged_tables.append(current_table)
                    current_table = table

        if current_table:
            merged_tables.append(current_table)

        logger.info(f"Stitching complete: {self.merge_count} merges, {len(merged_tables)} final tables")
        return merged_tables