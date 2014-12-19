CREATE VIEW daily_summary AS
	SELECT event, 
		time, 
		node, 
		incoming, 
		outgoing,
		summary.incoming + summary.outgoing AS overall,
		in_avg_velocity, 
		out_avg_velocity,
		(summary.in_sum_velocity + summary.out_sum_velocity) / (summary.incoming + summary.outgoing) AS avg_velocity,
		in_min_velocity,
		out_min_velocity,
		CASE 
			WHEN summary.in_min_velocity < summary.out_min_velocity 
				THEN summary.in_min_velocity 
				ELSE summary.out_min_velocity
		END AS min_velocity,
		in_max_velocity,
		out_max_velocity,
		CASE 
			WHEN summary.in_max_velocity > summary.out_max_velocity 
				THEN summary.in_max_velocity 
				ELSE summary.out_max_velocity
		END AS max_velocity
	FROM
		(SELECT coalesce(capsules_in.event, capsules_out.event) AS event,
			coalesce(capsules_in.time, capsules_out.time) AS time,
			coalesce(capsules_in.node, capsules_out.node) AS node, 
			coalesce(capsules_in.count, 0) AS incoming,
			coalesce(capsules_out.count, 0) AS outgoing,
			coalesce(capsules_in.avg_velocity, 0) AS in_avg_velocity,
			coalesce(capsules_out.avg_velocity, 0) AS out_avg_velocity,
			coalesce(capsules_in.sum_velocity, 0) AS in_sum_velocity,
			coalesce(capsules_out.sum_velocity, 0) AS out_sum_velocity,
			coalesce(capsules_in.min_velocity, 0) AS in_min_velocity,
			coalesce(capsules_out.min_velocity, 0) AS out_min_velocity,
			coalesce(capsules_in.max_velocity, 0) AS in_max_velocity,
			coalesce(capsules_out.max_velocity, 0) AS out_max_velocity
			
		FROM
			(SELECT event, 
				date_trunc('day', time) AS time, 
				destination AS node, 
				count(*) AS count,
				avg(velocity) AS avg_velocity,
				sum(velocity) AS sum_velocity,
				min(velocity) AS min_velocity,
				max(velocity) AS max_velocity
			FROM capsules GROUP BY event, destination, date_trunc('day', time)) capsules_in
		FULL OUTER JOIN
			(SELECT event,
				date_trunc('day', time) AS time, 
				origin AS node, 
				count(*) AS count,
				avg(velocity) AS avg_velocity,
				sum(velocity) AS sum_velocity,
				min(velocity) AS min_velocity,
				max(velocity) AS max_velocity
			FROM capsules GROUP BY event, origin, date_trunc('day', time)) capsules_out
		ON capsules_in.event = capsules_out.event 
			AND capsules_in.time = capsules_out.time 
			AND capsules_in.node = capsules_out.node) summary;
