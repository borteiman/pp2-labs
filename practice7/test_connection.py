from connect import connect

conn = connect()

if conn is not None:
    print("Test passed")
    conn.close()
else:
    print("Test failed")