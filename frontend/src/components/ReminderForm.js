import React, { useState } from 'react';
import axios from 'axios';

function ReminderForm({ userId, onReminderAdded }) {
  const [title, setTitle] = useState('');
  const [reminderTime, setReminderTime] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/reminder', {
        user_id: userId,
        title,
        reminder_time: reminderTime,
      });
      alert('Reminder added!');
      setTitle('');
      setReminderTime('');
      if (onReminderAdded) onReminderAdded();
    } catch (err) {
      alert(err.response?.data?.message || 'Error adding reminder');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-3 bg-light rounded">
      <div className="mb-3">
        <label className="form-label">Názov pripomienky</label>
        <input
          type="text"
          className="form-control"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Čas pripomienky (HH:MM:SS)</label>
        <input
          type="time"
          className="form-control"
          value={reminderTime}
          onChange={(e) => setReminderTime(e.target.value)}
          required
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Pridať
      </button>
    </form>
  );
}

export default ReminderForm;
