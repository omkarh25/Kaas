import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-6xl font-bold mb-8">
          Welcome to Kaas App
        </h1>
        <p className="text-xl mb-8">
          Manage your company's financial data with ease.
        </p>
        <div className="flex flex-wrap items-center justify-around max-w-4xl mt-6 sm:w-full">
          <Link href="/assets" className="p-6 mt-6 text-left border w-96 rounded-xl hover:text-blue-600 focus:text-blue-600">
            <h3 className="text-2xl font-bold">Assets &rarr;</h3>
            <p className="mt-4 text-xl">
              Manage your company's assets and track their value.
            </p>
          </Link>
          <Link href="/transactions" className="p-6 mt-6 text-left border w-96 rounded-xl hover:text-blue-600 focus:text-blue-600">
            <h3 className="text-2xl font-bold">Transactions &rarr;</h3>
            <p className="mt-4 text-xl">
              Record and manage financial transactions.
            </p>
          </Link>
          {/* Add more links for other features here */}
        </div>
      </main>
    </div>
  );
}
