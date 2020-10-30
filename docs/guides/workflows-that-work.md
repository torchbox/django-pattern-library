# Workflows that work

The workflow of developing UI components in a pattern library can be quite different from one-off templates that are only rendered where they are used. Here are tips to make the most of it.

## Keep the pattern library in sync

One of the upsides of having the pattern library built with Django is that the HTML templates can never go out of sync – but the data can! Make sure your template context and tag overrides keep in sync with your actual templates. This can for example be part of a code review checklist.

## Document your patterns

Patterns support defining a custom `name` in YAML, as well as rendering fully-fledged documentation in Markdown. Create a file next to the template to document it:

```markdown
This template can be used in different places. In streamfield block
or directly in a page template. To use this template pass `call_to_action` into context.

Example:

{% include "patterns/molecules/cta/call_to_action.html" with call_to_action=call_to_action %}
```

## Back-end first

Traditionally, Django development starts from models and everything else is derived from it. This is very natural from a back-end perspective – first define your data model, then the view(s) that reuse it, and finally templates.

We generally recommend this approach, but keep in mind that:

- With this workflow it’s natural to write templates that are heavily tied to the database structure, and as such not very reusable, and may be out of touch with visual design (which generally uses basic data structures like lists and mappings)
- There will be work to do to reconcile the data structure as defined by the back-end, with what is mandated by the designs.

To mitigate this effort, and overall make templates more reusable, take the time to massage data into simple structures that map better to visual representations.

## Front-end first

Alternatively, the pattern library makes it possible to write templates without models and views. This can be very convenient if your project’s schedule requires this kind of progression.

With this approach, keep in mind that:

- When creating the template from UI principles, there will be assumptions made about the underlying data structures to be provided by Django. Templates will be heavily tied to their visual design (which generally uses basic data structures like lists and mappings), and may be out of touch with the models once they are created.
- There will be work to do to reconcile the data structure as defined in the UI components, with what is mandated by the models.

To mitigate this effort, and overall make templates more reusable, take the time to massage data into simple structures that map better to visual representations.
