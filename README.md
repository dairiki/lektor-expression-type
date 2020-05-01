# Lektor Expression Type Plugin

Add jinja-evaluated types, `expression` and `format_expression`, to
[Lektor][].

These allow one to define data model fields whose values are Jinja2
expressions.

## The Types

Both the `expression` and `format_expression` types are evaluated by
the jinja template engine.

**`expression`**

The `expression` type is evaluated as a Jinja2 expression.

An example value for this type might be:
```
this.children.order_by('-pub_date').limit(4)
```
This would evaluate to a Lektor [Query][] instance.

**`format_expression`**

The `format_expression` type is evaluated as a Jinja2 template.  It
will always evaluate to a string.

An example value for this type might be:
```
The blog contains {{ site.get('/blog').count() }} pages.
```

## Installation

Add lektor-expression-type to your project from command line:

```
lektor plugins add lektor-expression-type
```

See [the Lektor plugin documentation][plugins] for more information.

## Motivating Example

Suppose you want to create an _Index_ data model, for pages which will
be used display lists of other pages on your site.
You could create a model definition like this (called, perhaps,
`models/index.ini`):


```ini
[model]
name = Index Page
label = Index: {{ this.title}}

[fields.title]
label = Title
type = string

[fields.items]
label = Items
type = expression
description = Pages to list on this page
```

In a particular index page which uses this model, you might set the
`items` field to
`site.get('/projects').filter(F.tag == 'interesting')`,
then in the page template (e.g. in `templates/index.html`) one could
reference the `items` field (e.g. `{% for page in this.items %}`)
to determine which pages to display on the page.

## Author

Jeff Dairiki <dairiki@dairiki.org>


[Lektor]: <https://www.getlektor.com/> "Lektor Static Content Management System"
[plugins]: <https://www.getlektor.com/docs/plugins/>
[Query]: <https://www.getlektor.com/docs/api/db/query/>
