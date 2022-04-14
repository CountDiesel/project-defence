from datetime import datetime, timedelta


def check_selected_slot_is_valid(event):
    if not event.date > datetime.now():
        return False

    c = []
    for x in range(len(event.doctor_id.days)):
        c.append(int(event.doctor_id.days[x]))
    if not event.date.weekday() in c:
        return False

    slot = datetime.combine(event.date, event.doctor_id.first_day_slot)
    day = [slot]
    time_change = timedelta(minutes=event.doctor_id.manipulation_duration)
    for x in range(event.doctor_id.manipulation_per_day):
        slot += time_change
        day.append(slot)
    if event.date not in day:
        return False

    return True

