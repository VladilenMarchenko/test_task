import React from 'react';
import {RouterNames} from "../../pages/RouterNames";
import css from "./Header.module.css";
import {Link} from "react-router-dom";

const Header = () => {
    return (
        <div className={css.header}>
            {Object.entries(RouterNames).map(([key, route]) => (
                <Link key={key} to={route.path} style={{marginRight: '1rem'}}>
                    {route.label}
                </Link>
            ))}
        </div>
    );
};

export default Header;