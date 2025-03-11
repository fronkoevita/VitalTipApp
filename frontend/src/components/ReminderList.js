import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ReminderList({ userId }) {
  const [reminders, setReminders] = useState([]);

  const fetchReminders = async () => {
    try {
      const res = await axios.get(`/api/reminders/${userId}`);
      setReminders(res.data.reminders);
    } catch (err) {
      alert(err.response?.data?.message || 'Error fetching reminders');
    }
  };

  useEffect(() => {
    fetchReminders();
    // eslint-disable-next-line
  }, [userId]);

  return (
    <div className="mt-3">
      <h4>Moje pripomienky</h4>
      {reminders.map((r) => (
        <div key={r.id} className="p-2 bg-light mb-2">
          <strong>{r.title}</strong> o {r.reminder_time}
          {r.active ? '' : ' (neaktívne)'}
        </div>
      ))}
    </div>
  );
}

export default ReminderList;
