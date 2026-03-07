import { getSession } from '@/lib/auth';
import { redirect } from 'next/navigation';
import LanguageSelector from '@/components/LanguageSelector';
import ProfileMenu from '@/components/ProfileMenu';
import ThemeToggle from '@/components/ThemeToggle';
import Breadcrumbs from '@/components/Breadcrumbs';
import DiagnosisHistoryClient from '@/components/DiagnosisHistoryClient';
import { getDatabase } from '@/lib/mongodb';
import { ObjectId } from 'mongodb';
import Link from 'next/link';

export default async function DiagnosisHistoryPage() {
  const session = await getSession();
  
  if (!session) {
    redirect('/login');
  }

  const db = await getDatabase();
  const user = await db.collection('users').findOne({ _id: new ObjectId(session.userId) });

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#0a0e27] text-slate-900 dark:text-white transition-colors duration-300">
      <nav className="border-b border-black/5 dark:border-white/5 bg-white/80 dark:bg-white/5 backdrop-blur-xl sticky top-0 z-50 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 sm:py-4 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2 sm:gap-3 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-gradient-to-br from-red-500 to-red-700 rounded-lg flex items-center justify-center font-bold text-base sm:text-lg rotate-45">
              <span className="-rotate-45">+</span>
            </div>
            <span className="text-lg sm:text-xl font-bold tracking-tight notranslate">EmerMedi</span>
          </Link>
          
          <div className="flex items-center gap-2 sm:gap-4">
            <ThemeToggle />
            <LanguageSelector />
            <ProfileMenu userName={user?.name} />
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <Breadcrumbs items={[{ label: 'Diagnosis History' }]} />
        
        <div className="mb-6 sm:mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold mb-2">Diagnosis History</h1>
          <p className="text-slate-600 dark:text-gray-400 text-sm sm:text-base">
            View all your emergency diagnosis records
          </p>
        </div>

        <DiagnosisHistoryClient />
      </main>
    </div>
  );
}
