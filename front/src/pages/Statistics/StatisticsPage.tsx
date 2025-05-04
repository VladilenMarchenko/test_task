import React, { useEffect, useState } from 'react';
import { api } from "../../http";
import css from './StatisticsPage.module.css';

const StatisticsPage = () => {
    const [amountImages, setAmountImages] = useState<number>(0);

    const getAmountImages = async () => {
        try {
            const response = await api.get("/vectors/count", {
                params: {
                    index_name: "image_vectors"
                }
            });
            setAmountImages(response.data);
        } catch (error) {
            console.error("Failed to fetch image count", error);
        }
    };

    useEffect(() => {
        getAmountImages();

        const interval = setInterval(() => {
            getAmountImages();
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className={css.statistics_container}>
            <h2 className={css.title}>Dataset Statistics</h2>
            <div className={css.stat_block}>
                <p className={css.stat_label}>Total images vectorized:</p>
                <p className={css.stat_value}>{amountImages}</p>
            </div>
        </div>
    );
};

export default StatisticsPage;