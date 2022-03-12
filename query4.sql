SELECT *
FROM(
	SELECT paper_referenced as paper_being_cited,count(*) AS cited_count
	FROM reference_table
	GROUP BY paper_referenced
	ORDER BY cited_count DESC 
	LIMIT 20) as sel_pid
JOIN research_paper ON (research_paper.paper_id=sel_pid.paper_being_cited)
