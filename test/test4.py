



def write_to_cassandra(input):
    from cassandra.cluster import Cluster
    cluster = Cluster(['52.20.47.196'])
    session = cluster.connect('playground')
    session.execute(
    """
    INSERT INTO users (name, credits, user_id)
    VALUES (%s, %s, %s)
    """,
    (input[0][0], input[0][1], input[1])
    )
    # stmt = "INSERT INTO tt (user_id, created_at) VALUES (%s, %s)"
    stmt = "INSERT INTO test_hourly (event_time, garage_name, availability) VALUES (%s, %s,%s)"
    session.execute(stmt, parameters=[input[0][0], input[0][1], input[1]])
    response = session.execute(stmt, parameters=[12, 'ab',2])
    print response
