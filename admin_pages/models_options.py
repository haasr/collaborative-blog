class NewsletterOptions:
    SEND_INTERVALS = (
        ('week', 'Each week'),
        ('month', 'Each month'),
    )

    WEEK_SEND_DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    SEND_HOURS = [ [i, f"{i} AM"] if (i-12)<0 else [i, f"{i-12} PM"] for i in range(0, 24) ]
    SEND_HOURS[0][1] = "12 AM" # Change from 0 AM to 12 AM
    SEND_HOURS[12][0] = 12 # Change 0 to 12
    SEND_HOURS[12][1] = "12 PM" # Change from 0 PM to 12 PM
    SEND_MINS = [ [i, f"{i}"] for i in range(0, 60, 10) ] # 0, 10 ... 60
    SEND_MINS[0][1] = f"00" # Keep 2-digit format -- '0' --> '00'
    NUM_FEATURED_POSTS = [ (i, i) for i in range(0, 4) ]
    NUM_RECENT_POSTS = [ (i, i) for i in range(0, 4) ]