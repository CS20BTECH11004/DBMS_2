SELECT 
	rp_cited.paper_id AS cited_id,rp_cited.paper_title,
	rp_citer.paper_id AS citer_id,rp_citer.paper_title,pap_nam.author_list,rp_citer.year,rp_citer.venue,rp_citer.abstract
FROM 
	research_paper AS rp_citer
	JOIN reference_table AS ref1 ON rp_citer.paper_id=ref1.paper_id
	JOIN research_paper AS rp_cited ON rp_cited.paper_id=ref1.paper_referenced
	LEFT JOIN (
		SELECT ag.paper_id as pap,string_agg(ai.first_name||' '||ai.middle_name||' '||ai.last_name,', ') AS author_list
		FROM 
			author_info as ai JOIN author_group as ag ON ai.author_id=ag.author_id
		GROUP BY ag.paper_id
	) AS pap_nam ON rp_citer.paper_id=pap_nam.pap
ORDER BY rp_cited.paper_id