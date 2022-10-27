# How to test addon locally

To run this addon locally for development purposes, follow these instructions:

Adding FEA addon panel:

- Create a new “test_add_{name}.py” file under “tests” directory
    - You can copy from my sample file “igor”
- Modify “filesDir” to include where you saved this repo (Blender-addon-for-FEA/blender_fea)
- Next open blender and add a text editor
- Locate the file “test_add_{name}.py” and run it through text editor

Visualizing addon panel:

- If a pop up did not appear on the “panels” side within 3D view, click the small arrow on the top right corner (next to “options”)
- You should now see a “FEA” panel on the right side; click it.
    - You should now see something like this:

        assets/fea_panel.png

    