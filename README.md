# sitegen
[WIP] low-tech static website generator that I am building for personal website and side-projects.

heavily inspired by https://github.com/lowtechmag/solar_v2 and credit is given in each file where source code has been used and/or modified.

### [WIP]

The general structure of the generated website depends on the config.toml file. The file defines content categories that can be used throughout the project to structure, style, and determine custom behavior throughout the site. The content categories determine colorization of the dithered images that are used throughout the site. 

For the purpose of the personal site that I am using as a guinea pig, the general content categories are:

- digital-things 
- physical-things
- favorite-things

Color palettes are provided for each category and content is tagged by category. Images within 

#### Posts

Posts are organized in the `content/` folder and each post is contained in one folder. The expectation of the generator is that there will be one `.md` file per folder, along with any images used within the post. 

The `.md` file can contain a `.toml` header that holds front-matter which will be plugged into the templates in `layouts/` when the site is being generated.

