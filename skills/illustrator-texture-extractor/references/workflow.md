# Illustrator surface-texture extraction workflow

## Outcome and grouping modes

Default to one transparent PNG per physical product surface or orthographic product view. The canvas represents the full surface bounds, while the visible pixels contain only the applied graphics. Preserve the source orientation, relative spacing, color, and vector sharpness.

Use isolated-element mode only when the user explicitly asks for separate logos, icons, or marking groups. In that mode, a tight content crop with small safety padding is appropriate. Do not silently substitute isolated elements for a requested whole-surface texture.

Surface graphics may be described as silkscreen, laser engraving, embossing, printing, logo, certification, regulatory text, serial-number area, or port label. If the user informally asks for all “silkscreen textures,” include all model-relevant surface markings unless they limit the manufacturing process.

## 1. Establish live state

1. Confirm Illustrator has an open document and record its name, artboard rectangle, Illustrator version, and color space.
2. Keep the source active and unsaved. Note whether the title indicates recovery or unsaved changes.
3. If the user authorized disabling the script warning, run:

   ```jsx
   app.preferences.setBooleanPreference("ShowExternalJSXWarning", false);
   ```

   Restore with `true` only if requested.

## 2. Export a stable visual reference

Export the active artboard at moderate scale to a task-local working directory. Use it for visual reasoning and coordinate planning instead of repeatedly navigating the GUI.

Use Computer Use only when a dialog or visible application state cannot be reached through COM/JSX. Do not use it as the primary selection mechanism.

## 3. Inventory Illustrator objects

Generate JSON for `document.pageItems`. Capture at least:

- index, `typename`, parent type, and layer;
- `visibleBounds` and `geometricBounds`;
- fill, stroke, stroke width, opacity, hidden, locked, and clipping state;
- text contents when live text remains;
- child, path, and point counts.

Illustrator bounds are `[left, top, right, bottom]`; top is numerically greater than bottom. Use `visibleBounds` when painted strokes matter. Text may already be converted to paths, so do not rely on `TextFrame` or content search alone.

## 4. Identify surfaces before markings

First partition the drawing into physical product surfaces or numbered orthographic views. For each surface, determine:

- the full surface rectangle used for UV registration;
- every applied graphic that belongs on that surface;
- construction artwork that defines the rectangle but must not render;
- orientation implied by the source view.

The full surface rectangle normally comes from the outer product construction outline. Its geometry may be split across several rounded-corner paths, so union the relevant outline bounds when necessary. Keep this rectangle as coordinate metadata; do not add the outline to the export item list.

## 5. Select applied graphics

Use the page preview to mark approximate regions, then correlate them with the object inventory. Prefer complete top-level objects whose bounds and appearance match the visible marking.

Include:

- all logos, charging rings, icons, indicators, and port labels on the surface;
- power/capacity text, certification symbols, regulatory and warning text;
- serial-number/date-code areas and other engraving needed by the 3D material workflow.

Exclude:

- product-body outlines, seams, ports, and mechanical geometry;
- dimensions, arrows, extension lines, center lines, tolerances, and callout labels;
- color/process notes, manufacturing instructions, page borders, title blocks, and direction diagrams;
- duplicate reference illustrations and visual markup added to indicate targets.

Do not assume annotations are red/blue or that product markings are black/gray. Combine semantic role, position, bounds, hierarchy, stroke/fill behavior, and nearby context. Use color filtering only after the visual role is understood.

Preserve compound paths as compound paths. Duplicating child paths separately can destroy holes in letters and symbols.

## 6. Export a registered whole-surface texture

For each surface:

1. Store the source surface rectangle separately from the marking items.
2. Create a temporary RGB Illustrator document.
3. Duplicate only the selected top-level marking items into its active layer.
4. Measure one source item before duplication and its copy after duplication. Illustrator may translate coordinates between documents.
5. Map the source surface rectangle by that translation and use the mapped rectangle as the temporary artboard.
6. Export PNG24 with transparency and artboard clipping.
7. Close the temporary document with `SaveOptions.DONOTSAVECHANGES` and reactivate the source.

Coordinate mapping pattern:

```jsx
var sourceBounds = sourceItems[0].visibleBounds;
var copied = sourceItems[0].duplicate(tempDoc.activeLayer, ElementPlacement.PLACEATEND);
var copiedBounds = copied.visibleBounds;
var dx = copiedBounds[0] - sourceBounds[0];
var dy = copiedBounds[1] - sourceBounds[1];
var artRect = [
    sourceSurfaceRect[0] + dx,
    sourceSurfaceRect[1] + dy,
    sourceSurfaceRect[2] + dx,
    sourceSurfaceRect[3] + dy
];
tempDoc.artboards[0].artboardRect = artRect;
```

Compute direct vector export scale:

```text
scalePercent = targetLongEdgePx / artboardLongEdgePt * 100
```

Use:

```jsx
var options = new ExportOptionsPNG24();
options.antiAliasing = true;
options.transparency = true;
options.matte = false;
options.artBoardClipping = true;
options.horizontalScale = scalePercent;
options.verticalScale = scalePercent;
options.saveAsHTML = false;
```

For explicitly requested isolated-element mode, union the copied marking bounds and add a small transparent safety margin instead of using a surface rectangle.

## 7. Correct Illustrator pixel rounding

Illustrator can miss the requested long edge by several pixels, especially on narrow artboards. Measure the first PNG. If its actual long edge is `actualPx`, export again from vectors with:

```text
correctedScalePercent = originalScalePercent * targetPx / actualPx
```

This is a second vector rasterization, not bitmap resizing.

## 8. Verify every output

Numerically verify:

- exact requested long edge;
- RGBA mode and alpha extrema containing transparent and visible pixels;
- painted alpha bounds and edge clearances;
- no clipping at outermost painted pixels.

Visually verify on a checkerboard contact sheet and at original resolution:

- one file contains the complete surface marking set, not fragmented elements;
- spacing, scale, orientation, and surface registration match the source;
- compound-path holes and small text remain intact;
- no structure lines, dimensions, callouts, page furniture, or target markup appear.

A viewer may display transparent pixels as black. Confirm alpha numerically rather than inferring transparency from the viewer background.

## 9. Report

Link each PNG and state exact dimensions. Identify surfaces and manufacturing processes when known. State that the source was not saved and temporary documents were closed. If a candidate is ambiguous, export it separately and label it as a candidate instead of silently merging it into a confirmed texture.
