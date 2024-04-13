import * as React from 'react';
import { Button } from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import {IconButton} from '@mui/material';
import dayjs from 'dayjs';

function Calendar(props) {
  const [selectedDate, setSelectedDate] = React.useState(dayjs());

  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
  };

  const handleNextDay = () => {
    setSelectedDate(prevDate => prevDate.add(1, 'day'));
  };

  const handlePreviousDay = () => {
    setSelectedDate(prevDate => prevDate.subtract(1, 'day'));
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div>
      <IconButton onClick={handlePreviousDay} aria-label="previous day">
          <NavigateBeforeIcon />
        </IconButton>
        
        <DatePicker
          value={selectedDate}
          onChange={handleDateChange}
          renderInput={({ inputRef, inputProps, InputProps }) => (
            <div>
              <input ref={inputRef} {...inputProps} />
              {InputProps?.endAdornment}
            </div>
          )}
        />
        <IconButton onClick={handleNextDay} aria-label="next day">
          <NavigateNextIcon />
        </IconButton>
      </div>
    </LocalizationProvider>
  );
}

export default Calendar;
