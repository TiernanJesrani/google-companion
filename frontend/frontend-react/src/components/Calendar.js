import * as React from 'react';
import { Button } from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import DayjsUtils from '@date-io/dayjs';

function Calendar(props) {
  const [selectedDate, setSelectedDate] = React.useState(null);
  const [open, setOpen] = React.useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false)
};
  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
    handleClose();
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div>
        <Button variant="outlined" onClick={handleOpen}>{props.date}</Button>
        <DatePicker
          open={open}
          onOpen={handleOpen}
          onClose={handleClose}
          value={selectedDate}
          onChange={handleDateChange}
          renderInput={({ inputRef, inputProps, InputProps }) => (
            <div>
              {InputProps?.endAdornment} {/* This line ensures the calendar icon and clear icon are still usable */}
            </div>
          )}
        />
      </div>
    </LocalizationProvider>
  );
}

export default Calendar;
