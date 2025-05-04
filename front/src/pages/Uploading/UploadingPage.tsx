import React, {useState} from 'react';
import css from './UploadingPage.module.css';
import {api} from "../../http";

const UploadingPage = () => {
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
            setStatus(null);
            setError(null);
        }
    };

    const handleSubmit = async () => {
        if (!file) return;
        setError("");
        setStatus(null);

        const formData = new FormData();
        formData.append("file", file);

        try {
            setStatus("Uploading...");
            const response = await api.post("/images/process-data-set", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            setStatus("✅ " + response.data.message);
            setError(null);
        } catch (err) {
            setError("Upload failed.");
            setStatus(null);
        }
    };

    return (
        <div className={css.upload_container}>
            <h2 className={css.upload_title}>Upload Image Dataset (.zip)</h2>

            <label htmlFor="zip-upload" className={css.file_label}>
                Select .zip File
            </label>
            <input
                id="zip-upload"
                type="file"
                accept=".zip"
                onChange={handleFileChange}
                className={css.hidden_input}
            />

            {file && <p className={css.file_name}>{file.name}</p>}

            <button onClick={handleSubmit} disabled={!file} className={css.upload_button}>
                Upload & Process
            </button>

            {status && <p className={css.status_message}>{status}</p>}
            {error && <p className={css.error_message}>{error}</p>}
        </div>
    );
};

export default UploadingPage;