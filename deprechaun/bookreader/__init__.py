"""Code for converting accounting records into depreciable assets.

This code takes in asset information extracted from an accounting record, and is responsible for:

- checking conditions imposed by the Internal Revenue Code;
- making certain selections, such as a depreciation convention, that are made based on the aggregate of depreciable assets; and
- producing an ``Asset`` object for each depreciable asset.
"""

from .book_asset import BookAsset
