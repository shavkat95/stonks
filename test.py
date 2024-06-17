


num_comments = "1.6K"
if "K" in num_comments:
    num_comments = num_comments.replace("K", "")
    num_comments = float(num_comments)
    num_comments = num_comments * 1000
    num_comments = int(num_comments)

print(num_comments)