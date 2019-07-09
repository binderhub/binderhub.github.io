---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

{% for binder in site.data.binders %}
<div>
	<a href="{{ binder.name }}.html"><h2 class="reference-block-header">{{ binder.name }}</h2></a>
</div>
{% endfor %}
