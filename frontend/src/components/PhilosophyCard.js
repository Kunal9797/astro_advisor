import React from 'react';

function PhilosophyCard({ philosophy }) {
    return (
        <div className="card h-100 shadow-sm">
            <div className="card-body">
                <h3 className="card-title">{philosophy.name}</h3>
                <h6 className="card-subtitle mb-2 text-muted">Origin: {philosophy.origin}</h6>
                <p className="card-text">{philosophy.description}</p>
                <div className="mt-3">
                    <h6>Key Principles:</h6>
                    <ul className="list-group list-group-flush">
                        {philosophy.key_principles.map((principle, index) => (
                            <li key={index} className="list-group-item">{principle}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default PhilosophyCard;