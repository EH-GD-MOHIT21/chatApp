import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import clsx from "clsx";

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    '& > * + *': {
      marginLeft: theme.spacing(2),
    },
  },
}));

export default function Spinner() {
  const classes = useStyles();

  return (
    <div className={clsx(classes.root,"spinnerhandler")} id="spinnerhandler">
      <CircularProgress />
      {/* <CircularProgress color="secondary" /> */}
    </div>
  );
}