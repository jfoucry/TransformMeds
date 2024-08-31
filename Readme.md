# TransformMeds

This project works with [Pilldroid](https://github.com/jfoucry/pilldroid) and it
used to generate the embedded data.

It use several files from a French government website and transform it into
databases (with encoding change and csv steps). It add fake record too, for
testing.

The 2 `.sql` files contains the SQL request in order to test them in a database
visualization software.

The result, `drugs.db` have to be include into the asset directory of the
Pilldroid project.

Note: It a very bad python but for now, it works :-)

Create a virtualenv:

`# python3 -m venv .venv`

Then activate the virtualenv:

`# source venve/bin/activate`

And install all the required software :

`# python -m pip install -r requirements.txt`

Then you can use the `transfromMeds.py` script.

To stop using the virtuelenv, use :

`# deactivate`

