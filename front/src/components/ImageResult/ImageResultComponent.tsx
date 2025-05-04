import React, {FC} from 'react';
import Image from "../Image/Image";
import {ImageResult} from "../../entities/ImageResult/type";
import css from "./ImageResult.module.css"

interface ImageResultComponentProps {
    imageResult: ImageResult
}

const ImageResultComponent: FC<ImageResultComponentProps> = ({imageResult}) => {
    return (
        <div className={css.container}>
            <Image src={imageResult.file_url}/>
            <p className={css.filename}>
                <span>Filename:</span>
                {imageResult.original_filename}</p>
            <p className={css.score}>
                <span> Score:</span> {imageResult.score.toFixed(4)}
            </p>
            <a className={css.download_link} href={process.env.REACT_APP_API + "/images/" + imageResult.file_url}
               rel="noreferrer">
                Download
            </a>
        </div>
    );
};

export default ImageResultComponent;