# The Computational Geometry of Urban Navigation
### A Scalable Performance Analysis of Informed Search on the 302,066-Node Lucknow Network

![License](https://img.shields.io/badge/License-Proprietary-red.svg)
![C++](https://img.shields.io/badge/C++-17-blue.svg)
![OSM](https://img.shields.io/badge/Data-OpenStreetMap-green.svg)

## 📌 Project Overview
This repository contains the complete computational framework and analytical pipeline used to evaluate Shortest Path Problem (SSP) algorithms within the unique urban morphology of the Lucknow district. By leveraging a high-fidelity dataset of **302,066 nodes**, this research benchmarks the performance of **Uninformed (Dijkstra)** vs. **Informed (A*)** search algorithms using a Haversine-based admissible heuristic.

### Key Results:
- **Mean State-Space Reduction:** 78.13%
- **Computational Efficiency:** A* visits ~1,393 nodes/km vs. Dijkstra’s ~6,396 nodes/km.
- **Topological Discovery:** Identification of the "Gomti Riverine Bottleneck Paradox" and the "Cantonment Regularity Effect."

---

## 📄 Research Paper & Full Dataset
The detailed theoretical findings, mathematical proofs, and exhaustive geospatial analysis are available in the accompanying paper.

****
- **📥 [Download Research Paper (PDF)](https://drive.google.com/file/d/1LAscWCBEEsvUR1EpDBS2_7EXT01mYSMy/view?usp=sharing)**
- **📊 [Access Raw CSV Datasets](https://drive.google.com/file/d/1LAscWCBEEsvUR1EpDBS2_7EXT01mYSMy/view?usp=sharing)**
---

## 🛠 Tech Stack
- **Language:** C++17 (Optimized for high-performance graph traversal)
- **Data Parsing:** `Libosmium` (Fast OSM PBF binary handling)
- **Analytics:** Python 3.10 (Pandas, Seaborn, Scipy)
- **Heuristic:** Spherical Haversine Formula (Earth Curvature Admissible)

---

## 🚀 Repository Structure
- `/src`: C++ source code for the pathfinding engine.
- `/data`: Sample metadata and coordinate bounding boxes.
- `/analysis`: Python scripts (`main.py`) used for generating statistical figures.
- `/plots`: High-resolution regression and density visualizations.

---

## ⚖️ Intellectual Property & Usage Restrictions
**No credit goes to school (Army Public School Sardar Patel Marg, Lucknow).** This research was conducted entirely through independent self-study and rigorous empirical evaluation by the author.

****

### Copyright Notice
© 2026 **Prateek Tiwari**. All Rights Reserved.

- **Educational Usage:** Permission is granted for individual researchers/students for strictly non-commercial, personal study.
- **Institutional Prohibition:** Any school, university, or corporate entity is **strictly prohibited** from using, citing, or distributing this work for promotional, commercial, or institutional accreditation purposes without express written authorization.
- **No Institutional Attribution:** No academic institution shall claim credit for the production, supervision, or results of this research.

---

## 📧 Contact
For inquiries regarding the methodology or permission for extended usage:
- **Researcher:** Prateek Tiwari
- **Email:** prateektiwari258@gmail.com
- **Location:** Lucknow, Uttar Pradesh, India
