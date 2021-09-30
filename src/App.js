import logo from './logo.svg';
import './App.css';
import HomePage from './components/HomePage';
import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import LoginPage from './components/LoginPage';
import SignupPage from './components/SignupPage';
import ForgotPass from './components/ForgotPass';
import PassChanger from './components/PassChanger';
import Chat from './components/Chat';
import ChatPage from './components/ChatPage';
import PrivateChatRoom from './components/PrivateChatRoom';
import PrivateChat from './components/PrivateChat';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/about">
          <HomePage />
        </Route>
        <Route path="/users">
          <HomePage />
        </Route>
        <Route path="/login">
          <LoginPage />
        </Route>
        <Route path="/signup">
          <SignupPage />
        </Route>
        <Route path="/forgotpass">
          <ForgotPass />
        </Route>
        <Route exact path="/chat">
          <Chat />
        </Route>

        <Route exact path="/privatechat">
          <PrivateChat />
        </Route>

        <Route path="/validate/user=:user/token=:token">
          <PassChanger />
        </Route>
        <Route path="/chat/private/:roomname">
          <PrivateChatRoom />
        </Route>
        <Route path="/chat/:roomname">
          <ChatPage />
        </Route>
        <Route exact path="/">
          <HomePage />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
