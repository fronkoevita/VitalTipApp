import React, { useState } from 'react';
import ReminderForm from '../components/ReminderForm';
import ReminderList from '../components/ReminderList';

function Reminders() {
  const [userId, setUserId] = useState(1); // sem dáš reálne ID po registrácii, zatiaľ test

  const handleUserChange = (e) => {
    setUserId(e.target.value);
  };

  return (
    <div className="container mt-4">
      <h2>Pripomienky</h2>
      <div className="mb-3">
        <label className="form-label">Zadaj User ID:</label>
        <input
          type="number"
          className="form-control"
          value={userId}
          onChange={handleUserChange}
        />
      </div>
      <ReminderForm userId={userId} onReminderAdded={() => {}} />
      <ReminderList userId={userId} />
    </div>
  );
}

export default Reminders;
