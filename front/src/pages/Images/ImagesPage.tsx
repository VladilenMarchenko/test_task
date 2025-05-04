import React, {useState} from 'react';
import {api} from "../../http";
import ImageResultComponent from "../../components/ImageResult/ImageResultComponent";
import {ImageResult} from "../../entities/ImageResult/type";
import css from "./ImagePage.module.css"

const ImagesPage = () => {
    const [file, setFile] = useState<File | null>(null);
    const [result, setResult] = useState<ImageResult[]>([]);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            setPreviewUrl(URL.createObjectURL(selectedFile));
        }
    };

    const handleSubmit = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await api.post("/images/find", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setResult(response.data.result);
            setError(null);
        } catch (err: any) {
            setError(err.response.statusText);
            setResult([]);
            console.error(err);
        }
    };

    return (
        <div>
            <div className={css.search_container}>
                <h2>Find Similar Images</h2>

                <label htmlFor="file-upload" className={css.custom_file_input}>
                    Choose Image
                </label>
                <input
                    id="file-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className={css.hidden_input}
                />

                {file && (
                    <div className={css.preview_container}>
                        <img src={previewUrl!} alt="preview" className={css.preview_image} />
                        <p className={css.filename}>{file.name}</p>
                    </div>
                )}

                <button onClick={handleSubmit} disabled={!file}>
                    Upload & Search
                </button>

            </div>

           <div className={css.result_container}>
               {error && <h2 style={{color: "red"}}>{error}</h2>}
           </div>

            {result.length > 0 && (
                <div className={css.result_container}>
                    <h2>Results:</h2>
                    <div className={css.result_images}>
                        {result.map((item: ImageResult, index: number) => (
                            <ImageResultComponent imageResult={item}/>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImagesPage;