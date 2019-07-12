---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

{% assign binder_name = page.name | replace: ".md", "" %}
{% assign binder = site.data.binders | where:"name",binder_name | first %}
<div>
	<h1 class="reference-jump-header">{{ binder.name }}</h1>
	{% for page in binder.pages %}
	<h2 class="reference-block-header">{{ page.name }}</h2>
	<div class="card-grid " data-component="card-grid">
	  	<div class="card-grid-inner">
	  	{% if site.card_sort_field %}
	  		{% if site.card_sort_field2 %}
	  			{% assign cards_grouped = page.cards | group_by: site.card_sort_field %}
	  			{% assign cards_grouped = cards_grouped | sort: "name" %}
	  			{% assign cards = '' | split: '' %}
				{% for card_group in cards_grouped %}
					{% assign cards_sorted = card_group.items | sort: site.card_sort_field2 %}
					{% assign cards = cards | concat: cards_sorted %}
				{% endfor %}
  			{% else %}
				{% assign cards = page.cards | sort: site.card_sort_field %}
			{% endif %}
		{% else %}
			{% assign cards = page.cards %}
		{% endif %}
		{% for card in cards %}
		    <div class="card-grid-item">
		        <a href="{{ card.scryfall_uri }}">
		        	<img class="card lea border-black" src="{{ card.image_uris.normal }}" style="box-shadow: 1px 1px 6px rgba(0,0,0,0.45); z-index: 5;" title="{{ card.oracle_text | smartify }}" />
	        	</a>
		    </div>
		{% endfor %}
		</div>
	</div>
  	{% endfor %}
</div>
