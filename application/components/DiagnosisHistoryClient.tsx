'use client';

import { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Mic, Image as ImageIcon, Eye, Trash2, Loader2 } from 'lucide-react';
import DiagnosisDetailModal from './DiagnosisDetailModal';

interface DiagnosisRecord {
  _id: string;
  type: 'audio' | 'image';
  result: any;
  fileUrl: string;
  fileName: string;
  isEmergency: boolean;
  createdAt: string;
}

export default function DiagnosisHistoryClient() {
  const [history, setHistory] = useState<DiagnosisRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRecord, setSelectedRecord] = useState<DiagnosisRecord | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('/api/diagnosis-history');
      const data = await response.json();
      setHistory(data.history || []);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this diagnosis record?')) return;

    setDeleting(id);
    try {
      const response = await fetch(`/api/diagnosis-history?id=${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setHistory(history.filter(record => record._id !== id));
      }
    } catch (error) {
      console.error('Failed to delete record:', error);
      alert('Failed to delete record');
    } finally {
      setDeleting(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-red-600" />
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="bg-white/80 dark:bg-white/5 backdrop-blur-sm border border-black/5 dark:border-white/10 rounded-xl p-12 text-center">
        <div className="w-20 h-20 bg-black/5 dark:bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <AlertCircle className="w-10 h-10 text-slate-400" />
        </div>
        <h3 className="text-xl font-bold mb-2">No Diagnosis History</h3>
        <p className="text-slate-600 dark:text-gray-400 mb-6">
          You haven't performed any emergency diagnoses yet
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="grid gap-4">
        {history.map((record) => (
          <div
            key={record._id}
            className="bg-white/80 dark:bg-white/5 backdrop-blur-sm border border-black/5 dark:border-white/10 rounded-xl p-4 sm:p-6 hover:border-black/10 dark:hover:border-white/20 transition-all"
          >
            <div className="flex items-start gap-4">
              {/* Icon */}
              <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${
                record.isEmergency
                  ? 'bg-red-500/20 dark:bg-red-500/30'
                  : 'bg-green-500/20 dark:bg-green-500/30'
              }`}>
                {record.isEmergency ? (
                  <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
                ) : (
                  <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4 mb-2">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      {record.type === 'audio' ? (
                        <Mic className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      ) : (
                        <ImageIcon className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                      )}
                      <span className="text-sm font-medium text-slate-600 dark:text-gray-400 capitalize">
                        {record.type} Diagnosis
                      </span>
                    </div>
                    <h3 className={`text-lg font-bold ${
                      record.isEmergency
                        ? 'text-red-700 dark:text-red-400'
                        : 'text-green-700 dark:text-green-400'
                    }`}>
                      {record.isEmergency ? 'Emergency Detected' : 'No Emergency'}
                    </h3>
                  </div>
                  <span className="text-xs text-slate-500 dark:text-gray-500 whitespace-nowrap">
                    {new Date(record.createdAt).toLocaleDateString()} {new Date(record.createdAt).toLocaleTimeString()}
                  </span>
                </div>

                {/* Quick Info */}
                <div className="mb-4">
                  {record.type === 'audio' && (
                    <p className="text-sm text-slate-600 dark:text-gray-400">
                      Emotion: <span className="font-semibold">{record.result.emotion}</span> • 
                      Category: <span className="font-semibold">{record.result.category}</span>
                    </p>
                  )}
                  {record.type === 'image' && (
                    <p className="text-sm text-slate-600 dark:text-gray-400">
                      {record.result.reason}
                    </p>
                  )}
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  <button
                    onClick={() => setSelectedRecord(record)}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-all flex items-center gap-2"
                  >
                    <Eye className="w-4 h-4" />
                    <span>View Details</span>
                  </button>
                  <button
                    onClick={() => handleDelete(record._id)}
                    disabled={deleting === record._id}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-lg text-sm font-medium transition-all flex items-center gap-2 disabled:cursor-not-allowed"
                  >
                    {deleting === record._id ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Deleting...</span>
                      </>
                    ) : (
                      <>
                        <Trash2 className="w-4 h-4" />
                        <span>Delete</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedRecord && (
        <DiagnosisDetailModal
          record={selectedRecord}
          onClose={() => setSelectedRecord(null)}
        />
      )}
    </>
  );
}
