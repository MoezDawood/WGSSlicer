# How Filter Set Loading and Saving Works

## Overview

The app allows you to save your filter configurations and reload them later. This is useful when you have common filter sets you use repeatedly.

## How It Works

### Saving Filter Sets

1. **Create your filter criteria** using the dropdown menus
2. **Click "💾 Save Filters"** button (only appears when you have active filters)
3. **Enter a name** for your filter set (e.g., "BRCA_Panel_Genes", "Rare_Variants")
   - Name can only contain letters, numbers, hyphens, and underscores
4. **Click "Save"** to save the filter set

**Where are they saved?**
- Filter sets are saved as JSON files on the BCM server
- Location: Same directory as `WGS_Slicer_v2.py`
- Filename format: `SavedSlicerFilterSet_{your_filter_name}.json`
- Example: `SavedSlicerFilterSet_BRCA_Panel_Genes.json`

### Loading Filter Sets

1. **Select your CSV files** first (required)
2. **Scroll to "🔄 Load Saved Filter Set"** section
3. **Choose a saved filter set** from the dropdown menu
4. **Click "Load Selected Filter Set"** button
5. Your filter fields will be automatically populated!

**What gets loaded?**
- All field selections
- All operator selections (greater than, contains, etc.)
- All values you entered
- Multi-gene lists (for HUGO field)

## Important Notes

### File Location
Filter sets are saved on the **BCM server** where the app is running:
```
/storage/lupski/home/mdawood/SlicerToWebsite/WGSSlicer/SavedSlicerFilterSet_*.json
```

### Sharing Filter Sets
- ✅ Filter sets saved on the server are **accessible to all users** who run the app from that server
- ✅ If you save a filter set, other users can load it
- ⚠️ If you want to share filter sets with users on different servers, you'd need to copy the JSON files

### Filter Set Contents
Each saved filter set contains:
- Filter name
- Creation date
- All filter fields with their:
  - Field names
  - Operators
  - Values
  - Multi-gene lists (for HUGO field)

## Example Workflow

1. **First time**: Create filters for BRCA genes
   - Select HUGO field
   - Enter: BRCA1, BRCA2, TP53
   - Add other filters as needed
   - Click "Save Filters" → Name it "BRCA_Panel"

2. **Next time**: 
   - Select your CSV files
   - Load "BRCA_Panel" from the dropdown
   - Click "Load Selected Filter Set"
   - All your filters are automatically filled in!

3. **Modify if needed**:
   - After loading, you can still modify any filter
   - Add or remove fields
   - Then save as a new filter set or overwrite

## Troubleshooting

### "No saved filter sets found"
- Make sure you've saved at least one filter set first
- Check that JSON files exist in the script directory on the server

### Filter set doesn't load correctly
- Make sure you've selected CSV files first (required)
- Try refreshing the page and loading again
- Check that the JSON file isn't corrupted

### Can't save filter set
- Make sure you have at least one active filter (field selected with a value)
- Check that the filter name only contains letters, numbers, hyphens, and underscores
- Verify you have write permissions in the script directory

## Viewing Saved Filter Sets

To see what filter sets are available, check the server directory:

```bash
# On BCM server
cd ~/SlicerToWebsite/WGSSlicer
ls -la SavedSlicerFilterSet_*.json
```

## Manual Filter Set Management

If you want to manually create or edit filter sets, you can edit the JSON files directly. The format is:

```json
{
  "filter_name": "My_Filter_Set",
  "created_date": "2026-01-03T12:00:00",
  "fields": [
    {
      "field": "hugo",
      "value": "BRCA1, BRCA2",
      "gene_list": ["BRCA1", "BRCA2"],
      "is_multi_value": true,
      "operator": "multi_contains"
    },
    {
      "field": "gnomad_af",
      "value": "0.01",
      "operator": "less_than",
      "operator_index": 1,
      "is_multi_value": false
    }
  ]
}
```

