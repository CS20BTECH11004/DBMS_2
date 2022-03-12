SELECT 
	rp_cited.paper_id AS cited_id,rp_cited.paper_title,
	rp_citer_sq.paper_id AS citer_sq_id,rp_citer_sq.paper_title,pap_nam.author_list,rp_citer_sq.year,rp_citer_sq.venue,rp_citer_sq.abstract
FROM 
	reference_table AS ref1 
	JOIN research_paper AS rp_cited ON rp_cited.paper_id=ref1.paper_referenced
    JOIN (
		SELECT r2.paper_id,r2.paper_title,r2.venue,r2.year,r2.abstract,r1.paper_id as mid_man
		FROM 
			reference_table AS ref2
			CROSS JOIN research_paper AS r1 
			JOIN research_paper AS r2 ON ref2.paper_referenced=r1.paper_id and r2.paper_id=ref2.paper_id
	
	) AS rp_citer_sq ON rp_citer_sq.mid_man=ref1.paper_id
	
	LEFT JOIN (
		SELECT ag.paper_id as pap,string_agg(ai.first_name||' '||ai.middle_name||' '||ai.last_name,', ') AS author_list
		FROM 
			author_info as ai JOIN author_group as ag ON ai.author_id=ag.author_id
		GROUP BY ag.paper_id
	) AS pap_nam ON rp_citer_sq.paper_id=pap_nam.pap
ORDER BY rp_cited.paper_id