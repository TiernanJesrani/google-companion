import * as React from 'react';
import AspectRatio from '@mui/joy/AspectRatio';
import Button from '@mui/joy/Button';
import Chip from '@mui/material/Chip'
import Card from '@mui/joy/Card';
import CardContent from '@mui/joy/CardContent';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Popper from '@mui/material/Popper';
import Fade from '@mui/material/Fade';
import CommentRoundedIcon from '@mui/icons-material/CommentRounded';

const Space = (props) => {
    const [open, setOpen] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
        setOpen((prevOpen) => !prevOpen);
      };
    const canBeOpen = open && Boolean(anchorEl);
    const id = canBeOpen ? 'transition-popper' : undefined;

    const onClickButton = (event) => {
      if (props.button_title === 'Create new' && props.setShowCreate) {
          props.setShowCreate(true)
      }
    }

    return (
        <Card sx={{ width: 320 }}>
      <div>
        <Typography level="title-lg">{props.name}</Typography>
        <Typography level="body-sm">{props.date_created}</Typography>
        
        <IconButton
          aria-label="bookmark Bahamas Islands"          
          size="sm"
          sx={{ position: 'absolute', top: '0.875rem', right: '0.5rem' }}
          onClick={handleClick}
        >
        </IconButton>
        <Popper id={id} open={canBeOpen} anchorEl={anchorEl} transition>
        {({ TransitionProps }) => (
          <Fade {...TransitionProps} timeout={350}>
            <Box sx={{ border: 1, p: 1, bgcolor: 'background.paper' }}>
               <CommentRoundedIcon/>New message from Amirali
            </Box>
          </Fade>
        )}
      </Popper>
      </div>
      <AspectRatio minHeight="120px" maxHeight="200px">
        <img
          src={props.image}
          loading="lazy"
          alt=""
        />
      </AspectRatio>
      <CardContent orientation="horizontal">
        <div>
        <Stack direction="row" spacing={1} alignItems="center">
          {props.tags.map((tag) => (
            <Chip color="primary" label={tag} size="small" />
          ))
          }
        </Stack>
        </div>
        <Button
          variant="solid"
          size="md"
          color="primary"
          aria-label="Explore Bahamas Islands"
          sx={{ ml: 'auto', alignSelf: 'center', fontWeight: 600 }}
          onClick={onClickButton}
        >
          {props.button_title}
        </Button>
      </CardContent>
    </Card>
    );
}
export default Space;