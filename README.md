# Framework for Spatially Joining River Flowlines from Different Datasets for Data Bitranslation 
<hr style="border: 1px solid black; margin: 0;">  

### **River Flowlines Spatial Join (RiverJoin)**
<hr style="border: 1px solid black; margin: 0;">  

| | |
| --- | --- |
| <a href="https://sdml.ua.edu"><img src="https://sdml.ua.edu/wp-content/uploads/2023/01/SDML_logo_Sq_grey.png" alt="SDML Logo" width="1000"></a> | **RiverJoin** performs a spatial join that addresses differences in flowlines from different datasets (e.g. different flowline densities, the spatial offset) and bi-transfer data, carried by the flowlines, between the datasets. It can  spatially join any two linear river features from different sources, provided that there are fields indicating river connectivity (e.g., a unique reach identifier and its corresponding downstream reach).

**RiverJoin** was originally developed to align the reach flowlines between the NOAA OWP HAND-FIM Hydrofabric (FIM HF) and the ICESat-2 River Surface Slope (IRIS) dataset that uses the Surface Water and Ocean Topography (SWOT) River Database (SWORD) flowlines to carry its data, aiming to improve river slope data in FIM HF.

**RiverJoin** is implemented as a pure-Python Jupyter Notebook.

- Users set only a few fields and parameters to apply the framework to their datasets.
- Requires only flowline geometries and basic connectivity fields—no auxiliary data.
- Reproducible and adaptable across regions and datasets.

We have successfully tested joins between FIM HF and SWORD, FIM HF and GEOGLOWS (Group on Earth Observation Global Water Sustainability), and SWORD and GEOGLOWS. We are currently testing joins between SWORD and MERIT (Multi-Error-Removed Improved Terrain) Basins.

### How the framework works -- the case of joining FIM HF and SWORD
<hr style="border: 1px solid black; margin: 0;">  

The major steps in this framework are shown in Fig. 1.

**Step 1: Initial Searching Using a Buffer Zone** (Fig. 1a)

>A 100 m buffer is drawn around each SWORD flowline. Any FIM HF flowline whose midpoint falls within that buffer is selected. This helps exclude small nearby tributaries and ensures that about half the FIM HF flowline aligns with the SWORD reach.

**Step 2: Downstream Tracing to Fill Gaps (get the initially unextracted FIM HF flowlines)** (Fig. 1b)

>Using the HydroID (flowline unique identifier) and NextDownID (HydroID of the next downstream flowline) fields in FIM HF, downstream tracing is applied to connect flowlines that weren’t initially captured by the buffer but are part of the same river path. This helps recover flowlines that continue downstream along the SWORD reach.

**Step 3: Upstream and Missed Segments Recovery Using Transects** (Fig. 1c)

>To find the (likely unextracted) most upstream and missed FIM HF flowlines, perpendicular transects are generated at regular intervals along the SWORD flowlines. A FIM HF flowline is selected if it intersects with multiple transects or intersects with at least one transect and has a stream order ≥ 2. These serve as the default screening criteria, although users can customize the selection based on intersection count, stream order, or other relevant fields in the FIM HF dataset. This step ensures comprehensive coverage.

>**Planned enhancement:** Enable users specify their own filter expressions based on the dataset’s fields.

**Step 4: Combine All Matched Flowlines** (Fig. 1d)

>All FIM HF flowlines identified through steps 1–3 are merged into a single layer.

**Step 5: Final alignment and attribute join** (Fig. 1e)

>Evenly spaced points along each FIM HF flowline are used to find the nearest SWORD streamline(s). The reach_id of the most frequently matched SWORD flowline is assigned to the FIM HF attribute table. This common ID enables direct joining of IRIS slope data to FIM HF flowlines.

>**Planned enhancement:** Enforce stream-order consistency so a FIM HF flowline only matches SWORD flowlines of the same order (not n ± 1).

<img src="./images/Flowchart_SpatialJoin_ForTransferSlopeFromIRIS2FIMHF.png" alt="Flowchart" width="650" style="border: 1px solid black; padding: 1px;">

<em>Fig. 1. Flowchart of identifying and spatially joining FIM HF flowlines with corresponding SWORD flowlines. Middle-column sub-figures enlarge the dashed-line boxed areas in the third column.</em>

### **Tool Usage**
<hr style="border: 1px solid black; margin: 0;">  

**RiverJoin** is provided as a Jupyter Notebook (RiverJoin_Python_2.0.ipynb) that you can download, open, and run. The major steps above are implemented as individual functions. Users only need to set the paths and field names for their flowlines. Other parameters—e.g., buffer distance, transect spacing and length, filters for selecting flowlines that intersect transects, and number of nodes to find the corresponding target flowline(s)—can be tuned to the data or left untouched (at their default values).

In RiverJoin_Python_2.0.ipynb, the field parameters are preconfigured for joining the GEOGLOWS to SWORD. You can download the GEOGLOWS streamlines (VPU 715) [here](http://geoglows-v2.s3-website-us-west-2.amazonaws.com/#hydrography/vpu=715/) and the SWORD flowline GeoPackage for North America (NA) [here](https://zenodo.org/records/15299138). Then specify the local paths to both flowline layers in the notebook and run it.

### **Citing This Framework**
<hr style="border: 1px solid black; margin: 0;">  

Chen, Y., Cohen, S., Baruah, A., Devi, D., Dhital, S., Tian, D., & Munasinghe, D. (2025). Merging Remote Sensing Derived River Slope Datasets with High-Resolution Hydrofabrics for the United States. Scientific Data, 12(1), 1657.

### **Acknowledgements**
<hr style="border: 1px solid black; margin: 0;">  

| | |
| --- | --- |
| ![alt text](https://ciroh.ua.edu/wp-content/uploads/2022/08/CIROHLogo_200x200.png) | This is developed under the Surface Dynamics Modeling Lab (SDML) as part of a project funded by the National Oceanic & Atmospheric Administration (NOAA), awarded to the Cooperative Institute for Research to Operations in Hydrology (CIROH) through the NOAA Cooperative Agreement with The University of Alabama (NA22NWS4320003). |

### **For More Information**
<hr style="border: 1px solid black; margin: 0;">  

#### **If you encounter any issues while using the framework, feel free to contact us:**

<a href="https://geography.ua.edu/people/sagy-cohen/" target="_blank">Dr. Sagy Cohen</a>
 (sagy.cohen@ua.edu),
Dr. Yixian Chen (ychen223@ua.edu), Supath Dhital (sdhital@crimson.ua.edu)
