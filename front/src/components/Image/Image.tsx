import React, {FC} from 'react';
import css from "./Image.module.css"

interface ImageProps {
    src: string;
}

const Image: FC<ImageProps> = ({src}) => {
    return (
        <div className={css.container}>
            <img src={`${process.env.REACT_APP_API}/images/${src}`} className={css.image}/>
        </div>
    );
};

export default Image;