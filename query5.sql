SELECT
    a1.author_id,a1.first_name,a1.middle_name,a1.last_name,
	a2.author_id,a2.first_name,a2.middle_name,a2.last_name,
    pair.p_count as number_of_papers
FROM
    (
    SELECT
        ag1.author_id AS coauth1,
        ag2.author_id AS coauth2,
        COUNT(*) AS p_count
    FROM author_group AS ag1 JOIN author_group AS ag2 
		ON ag1.paper_id = ag2.paper_id and ag1.author_id < ag2.author_id
    GROUP BY ag1.author_id,ag2.author_id
    ) AS pair  	
	JOIN author_info AS a1 ON pair.coauth1 = a1.author_id
	JOIN author_info AS a2 ON pair.coauth2 = a2.author_id
WHERE 
	pair.p_count>1