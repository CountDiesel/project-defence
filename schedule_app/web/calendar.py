import calendar


class MyNewCalendar(calendar.HTMLCalendar):

    def formatday(self, day, weekday, m):
        meetings = [1, 4, 10, 22]

        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            if day in m:
                return '<td style="text-align: center; vertical-align: top;" width="150" height="150" class="%s"><a href="%d/">%d</a></td>' % (self.cssclasses[weekday], day, day)
            return '<td style="text-align: center; vertical-align: top;" width="150" height="150" class="%s">%d</td>' % (self.cssclasses[weekday], day)

    def formatweek(self, theweek, m):
        """
        Return a complete week as a table row.
        """
        # s1 = self.monthdays2calendar(2022, 3)
        s = ''.join(self.formatday(d, wd, m) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, m, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, m))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def show_week(self, theweek, m):

        v = []
        a = v.append
        a('<table border="2" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        a(self.formatweek(theweek, m))
        a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
        #
        # s = ''.join(self.formatday(d, wd, m) for (d, wd) in theweek)
        # return '<tr>%s</tr>' % s
