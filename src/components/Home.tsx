import ImageDropzone from "./ImageDropzone";
import EyeIcon from "./icons/EyeIcon";

export default function Home() {
  return (
    <div
      className="text-center p-10 h-screen w-screen"
      style={{
        backgroundImage:
          "url(https://github.com/benjiiross/EyeDetector/blob/main/public/background.jpg?raw=true)",
        backgroundSize: "cover",
      }}
    >
      <div className="flex justify-center items-center space-x-2">
        <EyeIcon />
        <h2 className="text-2xl font-semibold">EyeDetector</h2>
      </div>

      <h1 className="text-4xl font-bold">Upload an eye image here</h1>
      <h2 className="text-xl font-semibold mt-2 text-gray-500">
        Supported formats are .jpg, .jpeg, .png, max 4MB
      </h2>

      <div className="mt-5">
        <ImageDropzone />
      </div>
    </div>
  );
}
