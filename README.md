# Image annotations

Simple usage:

Fill a directory `images/` with various images to annotate.
Currently everything is horrifically fragile w.r.t. to file names and escaping, so you should avoid special characters in the names of any of the image files. (TODO: fix this.)

The simply run:

```
	$ python label_server.py
```

Then navigate to [http://localhost:9999/](http://localhost:9999) in a browser.

Saved annotations will be written to the `annotations/` directory (which will be created if it didn't previously exist).


