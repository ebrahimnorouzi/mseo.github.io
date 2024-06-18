dashboard/ ontologies/:
	mkdir -p $@

.PRECIOUS: dependencies
dependencies:
	#pip install networkx==2.6.2
	echo "No dependencies needed."

.PRECIOUS: run_dashboard
run_dashboard: | dependencies dashboard/ ontologies/
	obodash -C dashboard-config.yml

dashboard/analysis.html:
	jupyter nbconvert dashboard_analysis.ipynb  --no-input --execute --to html --output $@

dashboard/general.html:
	jupyter nbconvert general.ipynb  --no-input --execute --to html --output $@
dashboard/base_metrics.html:
	jupyter nbconvert base_metrics.ipynb  --no-input --execute --to html --output $@
dashboard/schema_and_graph_metrics.html:
	jupyter nbconvert schema_and_graph_metrics.ipynb  --no-input --execute --to html --output $@
dashboard/pitfalls.html:
	jupyter nbconvert pitfalls.ipynb  --no-input --execute --to html --output $@