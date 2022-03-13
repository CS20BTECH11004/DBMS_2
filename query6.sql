CREATE VIEW ref_clique_unsorted AS
SELECT ref1.paper_id AS R1, ref2.paper_id AS R2, ref2.paper_referenced AS R3
FROM reference_table ref1 JOIN reference_table ref2 ON ref2.paper_id = ref1.paper_referenced
WHERE EXISTS (SELECT *
            FROM reference_table AS ref3
            WHERE (((ref3.paper_id = ref1.paper_id) AND (ref3.paper_referenced = ref2.paper_referenced))
				   OR ((ref3.paper_id = ref2.paper_referenced) AND (ref3.paper_referenced = ref1.paper_id))));

CREATE VIEW ref_clique AS
SELECT LEAST(R1,R2,R3) AS A, R1+R2+R3 - LEAST(R1,R2,R3) - GREATEST(R1,R2,R3) AS B, GREATEST(R1,R2,R3) AS C
FROM ref_clique_unsorted
WHERE LEAST(R1,R2,R3)<>(R1+R2+R3 - LEAST(R1,R2,R3) - GREATEST(R1,R2,R3)) AND
		(R1+R2+R3 - LEAST(R1,R2,R3) - GREATEST(R1,R2,R3))<>GREATEST(R1,R2,R3) 
		AND GREATEST(R1,R2,R3)<>LEAST(R1,R2,R3);

CREATE VIEW author_clique_unsorted AS
SELECT ag1.author_id AS X, ag2.author_id AS Y, ag3.author_id AS Z
FROM ref_clique AS x 
		JOIN author_group ag1 ON x.A = ag1.paper_id
		JOIN author_group ag2 ON x.B = ag2.paper_id
		JOIN author_group ag3 ON x.C = ag3.paper_id;

CREATE VIEW author_clique AS
SELECT LEAST(X,Y,Z) AS sorted_x, X+Y+Z-LEAST(X,Y,Z) - GREATEST(X,Y,Z) AS sorted_y, GREATEST(X,Y,Z) AS sorted_z,
				COUNT(*) AS count_uniq
FROM author_clique_unsorted
WHERE LEAST(X,Y,Z)<>(X+Y+Z - LEAST(X,Y,Z) - GREATEST(X,Y,Z)) AND
		(X+Y+Z - LEAST(X,Y,Z) - GREATEST(X,Y,Z))<>GREATEST(X,Y,Z) 
		AND GREATEST(X,Y,Z)<>LEAST(X,Y,Z)
GROUP BY (sorted_x, sorted_y, sorted_z);

SELECT a.author_id AS x_id, a.first_name AS x_fn, a.middle_name AS x_mn,a.last_name AS x_ln,
        b.author_id AS y_id,  b.first_name AS y_fn, b.middle_name AS y_mn ,b.last_name AS y_ln,
        c.author_id AS z_id,  c.first_name AS z_fn, c.middle_name AS z_mn,c.last_name AS z_ln,
        cit.count_uniq AS repeat_count
FROM author_clique cit JOIN author_info a ON cit.sorted_x = a.author_id
                       JOIN author_info b ON cit.sorted_y = b.author_id
                       JOIN author_info c ON cit.sorted_z = c.author_id;
								