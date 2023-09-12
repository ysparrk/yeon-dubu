import {React, useEffect} from 'react';
import './App.css';
import GlobalStyle from "./styles/GlobalStyle";
import FirstMain from './components/Login/FirstMain';
import HouseNaverMap from './components/HouseFind/HouseNaverMap';
import CoupleImage from './components/Common/CoupleImage';
import AccountInputMessage from './components/AccountInputStart/AccountInputMessage';
import AccountInputHeader from './components/Common/AccountInputHeader';
import DepositAccountInputForm from './components/AccountInput/DepositAccountInputForm';
import WeddingDayInput from './components/WeddingDay/WeddingDayInput';
import styled from 'styled-components';
import ScoreInputHeader from './components/CreditScoreInput/ScoreInputHeader';
import ScoreInput from './components/CreditScoreInput/ScoreInput';


function App() {
  function setScreenSize() {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`); //"--vh"라는 속성으로 정의해준다.
  }

  window.addEventListener('resize', () => setScreenSize());
  return (
    
    <div className="App">
      <GlobalStyle />


      <ScoreInputHeader/>
      <ScoreInput/>
 

      
    </div>
  );
}

export default App;
