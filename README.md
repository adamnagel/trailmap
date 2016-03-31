# trailmap

What should be the vertices (nodes), and what should be the edges?

Well, the vertices should be landmarks and intersections. The edges should be trail fragments that have distances and elevation info. But I don't really want to capture data from the park service map that way, so maybe I'll elect to draw a different kind of model of the trail system first, then automatically transform it into the graph that I want.

Okay, so what should my trail data model look like? Landmarks and such tend to lie along trails, so I think I'd like to capture them as being part of a trail. I'll want to capture distance information too, so that means the trails will have to be directed, with a start and end point. Landmarks on the trail will be marked with their distances from the "head". As a convention, I'll consider the western-most ending point of a trail to be its "head".

What will trails have?
- Intersection
- Landmark
- Campground or Shelter

Because trailheads/parking lots could be associated with many trails, I'll model them as their own elements in the model. They'll have to mark whether they're the "head" or "tail" of the trail. 

Distances are in miles.

Let's try it.

TODO:
- What if two trails intersect twice, as with Maddron Bald and Albright Grove Loop?
- What's the effect of things with zero distance? Should we take such sets and make sure they connect to the same other non-zero distance nodes?
- Consolidate vertices if they already exist (see Cosby Campground which is created several times).
- What if a vertex has multiple types?
- Look for a de-pluralize library

Trail Data Resources:
https://en.wikipedia.org/wiki/Maddron_Bald_Trail
https://www.nps.gov/grsm/planyourvisit/upload/GSMNP-Map_JUNE14-complete4-2.pdf
https://en.wikipedia.org/wiki/Snake_Den_Ridge_Trail
https://en.wikipedia.org/wiki/Lower_Mount_Cammerer_Trail
http://www.summitpost.org/luftee-knob/401884

Graph Resources:
http://www.graphviz.org/pdf/neatoguide.pdf
http://networkx.github.io