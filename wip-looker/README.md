# WIP Solution Looker

## Overview

Example Looker project structure to surface the data extracted by the solution.

## Prerequisites

- Working Looker instance
- Looker [connection](https://cloud.google.com/looker/docs/connecting-to-your-db) with permissions to connect to BQ Dataset and table where data is extracted to.

## Config and deployment

- Edit constants in [manifest file](./looker-project/manifest.lkml) to point to your connection, dataset and table
- Adjust [view file](./looker-project/views/extraction_table.view.lkml) to be in line with your extracted data
