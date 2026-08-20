import RobotAvatar from "@/components/RobotAvatar";
import TalkButton from "@/components/TalkButton";

const Home = () => {
  return (
    <main className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-start px-4 py-4 sm:px-6 sm:py-6 md:px-8">
      <h1 className="text-1xl sm:text-1xl md:text-4xl font-bold mb-2 text-center">
        AI Robot Assistant
      </h1>

      <div className="w-full max-w-sm sm:max-w-xl md:max-w-3xl rounded-2xl sm:rounded-3xl bg-slate-900 shadow-xl overflow-hidden">
        <RobotAvatar />
      </div>

      
      <TalkButton/>
    </main>
  );
};

export default Home;