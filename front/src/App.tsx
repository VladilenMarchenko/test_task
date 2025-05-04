import React from 'react';
import AppRouter from "./pages/AppRouter";
import Header from "./components/Header/Header";

function App() {
    return (
        <div className="App">
            <Header/>
            <AppRouter/>
        </div>
    );
}

export default App;
