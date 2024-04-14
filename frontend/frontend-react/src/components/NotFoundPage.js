import * as React from 'react';
import { Button } from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import {IconButton} from '@mui/material';
import dayjs from 'dayjs';
import NotFound from '../static/images/notfound.jpeg'

function NotFoundPage(props) {
  
  return (
    <div>
      <h1>Page not found</h1>
      <img src={NotFound}/>
    </div>
  );
}

export default NotFoundPage;
